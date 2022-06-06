import multipleData from '@/mockData/multipleData'
import axios from 'axios'
export function getPoints(domains: any): Promise<any> {
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
        }
    }
    return axios(options)

}