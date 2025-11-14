"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

const modelPerformanceData = [
  {
    name: "Gradient Boosting",
    accuracy: 90.99,
    weight: 25.1,
    color: "#fca311" // Orange Web
  },
  {
    name: "SVM",
    accuracy: 90.79,
    weight: 25.1,
    color: "#14213d" // Oxford Blue
  },
  {
    name: "Neural Network",
    accuracy: 90.73,
    weight: 25.1,
    color: "#ffffff" // White
  },
  {
    name: "Random Forest",
    accuracy: 89.31,
    weight: 24.7,
    color: "#000000" // Black
  },
  {
    name: "Weighted Ensemble",
    accuracy: 91.33,
    weight: 100,
    color: "#fca311" // Orange Web
  }
];

const modelWeightsData = [
  { name: "Gradient Boosting", value: 25.1, color: "#fca311" },
  { name: "SVM", value: 25.1, color: "#14213d" },
  { name: "Neural Network", value: 25.1, color: "#ffffff" },
  { name: "Random Forest", value: 24.7, color: "#000000" }
];

export function ModelPerformanceChart() {
  return (
    <Card style={{ background: '#14213d', color: '#ffffff', border: '1px solid #fca311' }}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between" style={{ color: '#ffffff' }}>
          Model Performance Comparison
          <Badge 
            variant="outline" 
            style={{ 
              borderColor: '#fca311', 
              color: '#fca311',
              backgroundColor: '#000000' 
            }}
          >
            91.33% Best
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={modelPerformanceData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#fca311" opacity={0.3} />
            <XAxis 
              dataKey="name" 
              angle={-45}
              textAnchor="end"
              height={80}
              fontSize={12}
              tick={{ fill: '#ffffff' }}
            />
            <YAxis 
              domain={[85, 95]}
              tickFormatter={(value) => `${value}%`}
              tick={{ fill: '#ffffff' }}
            />
            <Tooltip 
              formatter={(value: number) => [`${value}%`, 'Accuracy']}
              contentStyle={{
                backgroundColor: '#000000',
                border: '1px solid #fca311',
                borderRadius: '8px',
                color: '#ffffff'
              }}
            />
            <Bar 
              dataKey="accuracy" 
              radius={[4, 4, 0, 0]}
            >
              {modelPerformanceData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} stroke="#fca311" strokeWidth={entry.color === '#ffffff' ? 2 : 0} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export function ModelWeightsChart() {
  const RADIAN = Math.PI / 180;
  const renderCustomizedLabel = ({
    cx, cy, midAngle, innerRadius, outerRadius, percent
  }: any) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(1)}%`}
      </text>
    );
  };

  return (
    <Card style={{ background: '#ffffff', color: '#000000', border: '1px solid #fca311' }}>
      <CardHeader>
        <CardTitle style={{ color: '#000000' }}>Model Weights in Ensemble</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={modelWeightsData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              stroke="#fca311"
              strokeWidth={2}
            >
              {modelWeightsData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} stroke="#fca311" strokeWidth={2} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value: number) => [`${value}%`, 'Weight']}
              contentStyle={{
                backgroundColor: '#000000',
                border: '1px solid #fca311',
                borderRadius: '8px',
                color: '#ffffff'
              }}
            />
            <Legend 
              wrapperStyle={{ color: '#000000' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}