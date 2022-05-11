export function getPoint(domian: string): Promise<number> {
    domian
    return new Promise((res, rej) => {
        rej
        setTimeout(() => {
            res(Number((Math.random() * (9 - (-9)) + (-9)).toFixed(2)))
        }, 1000);
    })
}