export interface Order {
    pizza: string;
}

export interface PreferenceSet {
    name: string;
    id: number;
    isCuurent: boolean;
    preferences: Prefernce[];
}

export interface Prefernce {
    toping: string;
    score: number;
}

