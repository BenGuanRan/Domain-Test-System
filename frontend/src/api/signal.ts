import signalData from '@/mockData/signalData'
import axios from 'axios'
export function getPoint(domain: string, type: string): Promise<any> {
    const options = {
        url: '/api/api/signal',
        params: {
            domain,
            type
        }
    }
    return axios(options)
}