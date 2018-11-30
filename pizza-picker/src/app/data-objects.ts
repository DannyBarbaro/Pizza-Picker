export interface Order {
    pizza: string;
}

export interface PreferenceSet {
    name: string;
    id: number;
    isCurrent: boolean;
    prefs: Preference[];
}

export interface Preference {
    toping: string;
    score: number;
}

