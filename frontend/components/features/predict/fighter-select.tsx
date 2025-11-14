"use client";

import { useState, useEffect } from "react";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem } from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Check, ChevronsUpDown, User } from "lucide-react";
import { cn } from "@/lib/utils";

interface Fighter {
  name: string;
  recent_weight_class: string;
  recent_age: number | null;
  height: number | null;
  reach: number | null;
  stance: string;
  wins: number;
  losses: number;
}

interface FighterSelectProps {
  value?: string;
  onSelect: (fighter: Fighter | null) => void;
  placeholder?: string;
  side?: "red" | "blue";
}

export function FighterSelect({ value, onSelect, placeholder = "Select fighter...", side = "red" }: FighterSelectProps) {
  const [open, setOpen] = useState(false);
  const [fighters, setFighters] = useState<Fighter[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load fighters from backend API
    fetch('http://localhost:8000/fighters')
      .then(res => res.json())
      .then(data => {
        setFighters(data.fighters || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading fighters:', err);
        // Fallback to local JSON file
        fetch('/fighters.json')
          .then(res => res.json())
          .then(data => {
            setFighters(data);
            setLoading(false);
          })
          .catch(err2 => {
            console.error('Error loading fighters from fallback:', err2);
            setLoading(false);
          });
      });
  }, []);

  const selectedFighter = fighters.find(fighter => fighter.name === value);

  return (
    <div className="space-y-2">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between"
            style={{
              backgroundColor: side === "red" ? "#fca311" : "#14213d",
              color: side === "red" ? "#000000" : "#ffffff",
              borderColor: "#fca311"
            }}
          >
            {value ? (
              <span className="flex items-center gap-2">
                <User className="h-4 w-4" />
                {value}
              </span>
            ) : (
              placeholder
            )}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent 
          className="w-[400px] p-0" 
          style={{ 
            backgroundColor: "#14213d", 
            border: "1px solid #fca311",
            color: "#ffffff"
          }}
        >
          <Command style={{ backgroundColor: "#14213d" }}>
            <CommandInput 
              placeholder="Search fighters..." 
              style={{ backgroundColor: "#14213d", color: "#ffffff" }}
            />
            <CommandEmpty style={{ color: "#ffffff", backgroundColor: "#14213d" }}>No fighters found.</CommandEmpty>
            <CommandGroup 
              className="max-h-[300px] overflow-y-auto"
              style={{ backgroundColor: "#14213d" }}
            >
              {loading ? (
                <CommandItem disabled>Loading fighters...</CommandItem>
              ) : (
                fighters.map((fighter) => (
                  <CommandItem
                    key={fighter.name}
                    onSelect={() => {
                      onSelect(fighter.name === value ? null : fighter);
                      setOpen(false);
                    }}
                    className="cursor-pointer hover:bg-gray-700"
                    style={{ 
                      color: "#ffffff", 
                      backgroundColor: "#14213d",
                      borderBottom: "1px solid #2d3748"
                    }}
                  >
                    <Check
                      className={cn(
                        "mr-2 h-4 w-4",
                        value === fighter.name ? "opacity-100" : "opacity-0"
                      )}
                      style={{ color: "#fca311" }}
                    />
                    <div className="flex-1">
                      <div className="font-medium" style={{ color: "#ffffff" }}>{fighter.name}</div>
                      <div className="text-sm" style={{ color: "#fca311" }}>
                        {fighter.recent_weight_class} • {fighter.wins}-{fighter.losses}
                        {fighter.recent_age && ` • ${Math.round(fighter.recent_age)} years old`}
                      </div>
                    </div>
                  </CommandItem>
                ))
              )}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </Popover>
      
      {selectedFighter && (
        <div className="mt-3 p-3 rounded-lg border" style={{ 
          backgroundColor: "#14213d", 
          borderColor: "#fca311",
          color: "#ffffff" 
        }}>
          <div className="flex flex-wrap gap-2 mb-2">
            <Badge style={{ backgroundColor: "#fca311", color: "#000000" }}>
              {selectedFighter.recent_weight_class}
            </Badge>
            <Badge variant="outline" style={{ borderColor: "#fca311", color: "#fca311" }}>
              {selectedFighter.wins}-{selectedFighter.losses}
            </Badge>
            {selectedFighter.stance !== "Unknown" && (
              <Badge variant="outline" style={{ borderColor: "#fca311", color: "#fca311" }}>
                {selectedFighter.stance}
              </Badge>
            )}
          </div>
          <div className="grid grid-cols-2 gap-2 text-sm">
            {selectedFighter.recent_age && (
              <div>
                <span style={{ color: "#fca311" }}>Age:</span> {Math.round(selectedFighter.recent_age)}
              </div>
            )}
            {selectedFighter.height && (
              <div>
                <span style={{ color: "#fca311" }}>Height:</span> {Math.round(selectedFighter.height)}cm
              </div>
            )}
            {selectedFighter.reach && (
              <div>
                <span style={{ color: "#fca311" }}>Reach:</span> {Math.round(selectedFighter.reach)}cm
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}