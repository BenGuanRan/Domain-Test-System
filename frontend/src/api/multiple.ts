import multipleData from '@/mockData/multipleData'
import axios from 'axios'
const CancelToken = axios.CancelToken;
export function getPoints(domains: any, store: any): Promise<any> {
    console.log(domains);
    const searchValues: { domain: any }[] = []
    domains.forEach((i: { domain: any }) => {
        searchValues.push(i.domain)
    })
    console.log(searchValues);
    const options = {
        url: '/api/api/multiple',
        params: {
            domains: searchValues.join('/'),
        },
        cancelToken: new CancelToken(function executor(c) {
            // executor 函数接收一个 cancel 函数作为参数
            store.state.cancelFunc = c;
        })
    }
    return axios(options)

}