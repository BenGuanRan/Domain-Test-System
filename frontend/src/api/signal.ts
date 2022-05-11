import signalData from '@/mockData/signalData'
export function getPoint(domian: string): Promise<Object> {
    return new Promise((res, rej) => {
        setTimeout(() => {
            res(signalData)
        }, 1000);
    })
}