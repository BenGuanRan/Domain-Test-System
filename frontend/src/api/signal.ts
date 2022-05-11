import signalData from '@/mockData/signalData'
export function getPoint(domian: string): Promise<any> {
    return new Promise((res, rej) => {
        setTimeout(() => {
            res(signalData)
        }, 2000);
    })
}