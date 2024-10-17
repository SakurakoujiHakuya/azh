const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = 3000;

// 设置 multer 用于处理文件上传
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'input');
    },
    filename: (req, file, cb) => {
        cb(null, 'pt.jpg');
    }
});
const upload = multer({ storage: storage });

// 上传图片的路由
app.post('/upload', upload.single('file'), (req, res) => {
    res.send('文件上传成功');
});

// 运行 Python 脚本的路由
app.post('/run-script', (req, res) => {
    exec('python moxingceshi/main.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`执行错误: ${error}`);
            return res.status(500).send('运行脚本时出错');
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
        res.send('脚本运行成功');
    });
});

// 提供静态文件
app.use('/output', express.static(path.join(__dirname, 'output')));

app.listen(port, () => {
    console.log(`服务器运行在 http://localhost:${port}`);
});