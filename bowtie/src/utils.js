export const storeState = (uuid, state, data) => {
    sessionStorage.setItem(uuid, JSON.stringify(Object.assign(state, data)));
};

export const str2ints = x => {
    return x.split(',').map(y => parseInt(y, 10));
};
