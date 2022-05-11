export function exportExcel(data: any, title: Array<string> = []) {
    let str = ''
    // 如果是数组
    if (data instanceof Array) {
        if (title.length == 0)
            title = Object.keys(data[0])
        // 列标题，逗号隔开，每一个逗号就是隔开一个单元格
        str = title.join(',') + '\n';
        // 增加\t为了不让表格显示科学计数法或者其他格式
        for (let i = 0; i < data.length; i++) {
            for (const key in data[i]) {
                str += `${data[i][key] + '\t'},`;
            }
            str += '\n';
        }


    }
    // 如果是对象
    else if (data instanceof Object) {
        if (title.length == 0)
            title = Object.keys(data)
        str = ""
        title.forEach(i => {
            str += `${i},${data[i]}\t\n`
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
    link.download = "json数据表.csv";
    link.click();
}