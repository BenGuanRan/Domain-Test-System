module.exports = {
    lintOnSave: false,
    devServer: {
        open: true,
        host: 'localhost',
        port: 8080,
        https: false,
        proxy: {
            '/api': {//请求称号
                target: 'http://localhost:8000/', //请求的接口
                ws: true,
                changeOrigin: true,//允许跨域
                pathRewrite: {
                    '^/api': ''
                }

            }

        }
    }


}