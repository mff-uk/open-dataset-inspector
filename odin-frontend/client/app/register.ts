/**
 * Holds information about registered components.
 */

const registered: Array<object> = [];

export function register(component: object) {
    registered.push(component);
}

export function getRegistered(): Array<object> {
    return registered;
}
