const XLSX = require("xlsx");

export function exportExcel(data: any, fileName = '数据表', title: Array<string> = []) {
    let str = ''
    
    // 如果是数组
    if (data instanceof Array) {
        const jsonWorkSheet = XLSX.utils.json_to_sheet(data);
        const workbook = {
            SheetNames: [fileName],
            Sheets: {
                [fileName]: jsonWorkSheet,
            }
        };
        return XLSX.writeFile(workbook, fileName + '.xlsx');
    }
    // 如果是对象
    else if (data instanceof Object) {
        if (title.length == 0)
            title = Object.keys(data)
        str = ""
        title.forEach(i => {
            str += `${i},${data[i]}\n`
        })


    } else {
        str = data.toString()
    }
    // encodeURIComponent解决中文乱码
    const uri = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(str);
    // 通过创建a标签实现
    const link = document.createElement("a");
    link.href = uri;
    // 对下载的文件命名
    link.download = fileName + '.csv';
    link.click();
}