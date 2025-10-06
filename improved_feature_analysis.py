def analyze_success_factors(self):
        """
        Analyze what factors contribute most to fighter success using multiple methods:
        1. SHAP values for detailed feature impact
        2. Cross-validated XGBoost importance
        3. Feature interactions
        4. Bootstrap confidence intervals
        """
        import shap
        from scipy import stats
        from sklearn.model_selection import KFold
        
        # Create more comprehensive success metric
        self.df['success_score'] = (
            self.df['win_rate'] * 0.5 +                    # Win rate
            (self.df['wins'] / self.df['wins'].max()) * 0.3 +  # Normalized total wins
            (1 - self.df['losses'] / self.df['wins'].max()) * 0.2  # Normalized loss prevention
        )
        
        # Prepare features with interactions
        X = self.df[self.feature_columns + ['stance_encoded']]
        
        # Add interaction features
        X['striking_efficiency'] = self.df['slpm'] * self.df['sig_str_acc']
        X['grappling_efficiency'] = self.df['td_avg'] * self.df['td_acc']
        X['defensive_ability'] = self.df['str_def'] * self.df['td_def']
        X['physical_advantage'] = (self.df['height'] * self.df['weight'] * self.df['reach']) ** (1/3)
        
        y = self.df['success_score']
        
        # Initialize results storage
        feature_importances = []
        shap_values_global = None
        cv_scores = []
        
        # Cross-validation for robust feature importance
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        
        for train_idx, val_idx in kf.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            # Train model
            model = XGBRegressor(
                n_estimators=100,
                learning_rate=0.05,
                max_depth=5,
                random_state=42
            )
            model.fit(X_train, y_train)
            
            # Calculate SHAP values
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_val)
            
            if shap_values_global is None:
                shap_values_global = shap_values
            else:
                shap_values_global = np.vstack([shap_values_global, shap_values])
            
            # Store feature importance
            feature_importances.append(model.feature_importances_)
            
            # Calculate validation score
            score = model.score(X_val, y_val)
            cv_scores.append(score)
        
        # Calculate confidence intervals for feature importance
        feature_importance_matrix = np.array(feature_importances)
        mean_importance = feature_importance_matrix.mean(axis=0)
        ci_lower = np.percentile(feature_importance_matrix, 2.5, axis=0)
        ci_upper = np.percentile(feature_importance_matrix, 97.5, axis=0)
        
        # Prepare results DataFrame
        results = pd.DataFrame({
            'feature': X.columns,
            'importance_mean': mean_importance,
            'importance_ci_lower': ci_lower,
            'importance_ci_upper': ci_upper,
            'shap_importance': np.abs(shap_values_global).mean(axis=0)
        })
        
        # Calculate stability score (how consistent the feature ranking is across folds)
        stability_scores = []
        for i in range(len(X.columns)):
            rankings = [list(importance).index(importance[i]) 
                       for importance in feature_importances]
            stability = 1 - np.std(rankings) / len(X.columns)
            stability_scores.append(stability)
        
        results['stability_score'] = stability_scores
        
        # Sort by SHAP importance
        results = results.sort_values('shap_importance', ascending=False)
        
        # Create feature importance plots
        self.plot_enhanced_feature_importance(results, shap_values_global, X)
        
        return {
            'feature_importance': results,
            'model_cv_score': np.mean(cv_scores),
            'model_cv_std': np.std(cv_scores),
            'top_interactions': self.analyze_feature_interactions(X, y)
        }

    def analyze_feature_interactions(self, X, y):
        """Analyze interactions between features"""
        from itertools import combinations
        
        interactions = []
        features = X.columns
        
        for f1, f2 in combinations(features, 2):
            interaction = X[f1] * X[f2]
            corr = np.corrcoef(interaction, y)[0, 1]
            interactions.append({
                'features': (f1, f2),
                'interaction_strength': abs(corr)
            })
        
        return sorted(interactions, key=lambda x: x['interaction_strength'], reverse=True)[:10]

    def plot_enhanced_feature_importance(self, results, shap_values, X):
        """Create enhanced feature importance visualizations"""
        plt.figure(figsize=(15, 10))
        
        # Plot 1: Feature Importance with Confidence Intervals
        plt.subplot(2, 2, 1)
        plt.errorbar(
            range(len(results)), 
            results['importance_mean'],
            yerr=[
                results['importance_mean'] - results['importance_ci_lower'],
                results['importance_ci_upper'] - results['importance_mean']
            ],
            fmt='o'
        )
        plt.xticks(range(len(results)), results['feature'], rotation=45, ha='right')
        plt.title('Feature Importance with 95% Confidence Intervals')
        
        # Plot 2: SHAP Summary Plot
        plt.subplot(2, 2, 2)
        shap.summary_plot(
            shap_values, 
            X,
            plot_type='bar',
            show=False
        )
        plt.title('SHAP Feature Importance')
        
        # Plot 3: Stability Score
        plt.subplot(2, 2, 3)
        sns.barplot(
            x='feature',
            y='stability_score',
            data=results
        )
        plt.xticks(rotation=45, ha='right')
        plt.title('Feature Importance Stability Across Folds')
        
        # Plot 4: Feature Importance Distribution
        plt.subplot(2, 2, 4)
        sns.boxplot(data=pd.DataFrame(feature_importance_matrix, columns=X.columns))
        plt.xticks(rotation=45, ha='right')
        plt.title('Feature Importance Distribution Across Folds')
        
        plt.tight_layout()
        plt.savefig('feature_importance_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()