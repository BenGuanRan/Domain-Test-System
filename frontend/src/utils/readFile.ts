
import xlsx from 'xlsx';
export function resadFile(file: any): any {
    const workbook = xlsx.readFile(file);
    const res = xlsx.readFile(file);
    return res
}