import multipleData from '@/mockData/multipleData'
export function getPoints(domains: any): Promise<any> {
    return new Promise((res, rej) => {
        setTimeout(() => {
            res(multipleData)
        }, 200);
    })
}