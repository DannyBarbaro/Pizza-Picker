export interface Order {
    components: OrderComponent[];
}

export interface OrderComponent {
    toppings: string[];
    sliceCount: number;
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

