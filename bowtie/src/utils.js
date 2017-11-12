export const storeState = (uuid, state, data) => {
    sessionStorage.setItem(uuid, JSON.stringify(Object.assign(state, data)));
};
