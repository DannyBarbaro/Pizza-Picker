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
    topping: string;
    score: number;
}

