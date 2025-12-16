'use client';

import { useState, useEffect } from 'react';
import { useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';
import { Doc } from '@/convex/_generated/dataModel';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Search, User, Trophy, Weight, Ruler, Target } from 'lucide-react';

interface FighterSearchProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
}

export function FighterSearch({ value, onChange, placeholder = "Enter fighter name", disabled, error }: FighterSearchProps) {
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const [debouncedValue, setDebouncedValue] = useState(value);

  // Debounce the search term to avoid too many requests
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, 300);
    return () => clearTimeout(timer);
  }, [value]);

  const searchResults = useQuery(api.fighters.searchFighters, { searchTerm: debouncedValue });
  const suggestions: Doc<"fighters">[] = searchResults || [];

  useEffect(() => {
    if (value.length < 2) {
      setShowSuggestions(false);
      return;
    }

    const exactMatch = suggestions.some(f => f.name === value);
    setShowSuggestions(suggestions.length > 0 && !exactMatch);
    setHighlightedIndex(-1);
  }, [value, suggestions]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showSuggestions) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setHighlightedIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : 0
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setHighlightedIndex(prev => 
          prev > 0 ? prev - 1 : suggestions.length - 1
        );
        break;
      case 'Enter':
        e.preventDefault();
        if (highlightedIndex >= 0) {
          onChange(suggestions[highlightedIndex].name);
          setShowSuggestions(false);
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        setHighlightedIndex(-1);
        break;
    }
  };

  const selectSuggestion = (fighterName: string) => {
    onChange(fighterName);
    setShowSuggestions(false);
    setHighlightedIndex(-1);
  };

  return (
    <div className="relative">
      <div className="relative">
        <Search 
          className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4" 
          style={{ color: '#ff002b' }}
        />
        <Input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          className="pl-10"
          style={{ 
            backgroundColor: '#000000', 
            borderColor: error ? '#ef4444' : '#ff002b', 
            color: '#ffffff',
            boxShadow: '0 0 10px rgba(252, 163, 17, 0.1)'
          }}
        />
      </div>

      {showSuggestions && (
        <Card 
          className="absolute z-50 w-full mt-1 max-h-64 overflow-y-auto"
          style={{ backgroundColor: '#002962', border: '1px solid #ff002b' }}
        >
          <CardContent className="p-0">
            {suggestions.map((fighter, index) => {
              return (
                <button
                  key={fighter._id}
                  onClick={() => selectSuggestion(fighter.name)}
                  className={`w-full p-3 text-left hover:bg-opacity-20 hover:bg-gray-500 border-b border-gray-700 last:border-b-0 ${
                    index === highlightedIndex ? 'bg-opacity-20 bg-gray-500' : ''
                  }`}
                  style={{ color: '#ffffff' }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <User className="h-4 w-4" style={{ color: '#ff002b' }} />
                      <div>
                        <div className="font-medium">{fighter.name}</div>
                        <div className="text-xs text-gray-400 flex items-center space-x-3">
                          <span className="flex items-center space-x-1">
                            <Weight className="h-3 w-3" />
                            <span>{fighter.weightClass}</span>
                          </span>
                          <span className="flex items-center space-x-1">
                            <Trophy className="h-3 w-3" />
                            <span>{fighter.record.wins}-{fighter.record.losses}-{fighter.record.draws || 0}</span>
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-xs text-gray-500">
                      <Target className="h-3 w-3" />
                    </div>
                  </div>
                </button>
              );
            })}
          </CardContent>
        </Card>
      )}

      {error && (
        <div className="text-red-400 text-xs mt-1 flex items-center space-x-1">
          <span>⚠</span>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}

// Popular fighter suggestions by weight class
export const FIGHTERS_BY_WEIGHT_CLASS = {
  'Heavyweight': ['Jon Jones', 'Stipe Miocic', 'Francis Ngannou', 'Ciryl Gane', 'Curtis Blaydes'],
  'Light Heavyweight': ['Jiri Prochazka', 'Glover Teixeira', 'Jan Blachowicz', 'Anthony Smith', 'Thiago Santos'],
  'Middleweight': ['Israel Adesanya', 'Robert Whittaker', 'Paulo Costa', 'Marvin Vettori', 'Derek Brunson'],
  'Welterweight': ['Leon Edwards', 'Kamaru Usman', 'Colby Covington', 'Jorge Masvidal', 'Stephen Thompson'],
  'Lightweight': ['Islam Makhachev', 'Charles Oliveira', 'Justin Gaethje', 'Dustin Poirier', 'Michael Chandler'],
  'Featherweight': ['Alexander Volkanovski', 'Max Holloway', 'Brian Ortega', 'Calvin Kattar', 'Josh Emmett'],
  'Bantamweight': ['Aljamain Sterling', 'Sean O\'Malley', 'Henry Cejudo', 'Petr Yan', 'Cory Sandhagen'],
  'Flyweight': ['Brandon Moreno', 'Deiveson Figueiredo', 'Kai Kara-France', 'Alex Perez', 'Matt Schnell'],
  'Women\'s Bantamweight': ['Amanda Nunes', 'Holly Holm', 'Miesha Tate', 'Ketlen Vieira', 'Irene Aldana'],
  'Women\'s Flyweight': ['Valentina Shevchenko', 'Katlyn Chookagian', 'Jessica Andrade', 'Lauren Murphy', 'Viviane Araujo'],
  'Women\'s Strawweight': ['Zhang Weili', 'Rose Namajunas', 'Carla Esparza', 'Joanna Jedrzejczyk', 'Marina Rodriguez']
};