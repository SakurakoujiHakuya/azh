const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = 3000;

// 设置 multer 用于处理文件上传
const storageDiagnosis = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'input');
    },
    filename: (req, file, cb) => {
        cb(null, 'pt.jpg');
    }
});

const storageEncipher = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'input');
    },
    filename: (req, file, cb) => {
        cb(null, 'pt2.bmp');
    }
});

const storageDecrypt = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'input');
    },
    filename: (req, file, cb) => {
        cb(null, 'pt3.bmp');
    }
});

const uploadDiagnosis = multer({ storage: storageDiagnosis });
const uploadEncipher = multer({ storage: storageEncipher });
const uploadDecrypt = multer({ storage: storageDecrypt });

// 上传图片的路由
app.post('/upload-diagnosis', uploadDiagnosis.single('file'), (req, res) => {
    res.send('文件上传成功');
});

app.post('/upload-encipher', uploadEncipher.single('file'), (req, res) => {
    res.send('文件上传成功');
});

app.post('/upload-decrypt', uploadDecrypt.single('file'), (req, res) => {
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

app.post('/run-script-en', (req, res) => {
    exec('python moxingceshi/encryption.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`执行错误: ${error}`);
            return res.status(500).send('运行脚本时出错');
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
        res.send('脚本运行成功');
    });
});

app.post('/run-script-de', (req, res) => {
    exec('python moxingceshi/decryption.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`执行错误: ${error}`);
            return res.status(500).send('运行脚本时出错');
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
        res.send('脚本运行成功');
    });
});

app.post('/run-script-chart', (req, res) => {
    exec('python moxingceshi/NpcrUaciBaci.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`执行错误: ${error}`);
            return res.status(500).send('运行脚本时出错');
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
        res.send('脚本运行成功');
    });
});

app.post('/run-script-chartTwo', (req, res) => {
    exec('python moxingceshi/entropy_analysis.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`执行错误: ${error}`);
            return res.status(500).send('运行脚本时出错');
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
        res.send('脚本运行成功');
    });
});

//key
// app.post('/save-dialog-values', (req, res) => {
//     const { filePath, data } = req.body;

//     // 确保目录存在
//     const fullPath = path.join(__dirname, filePath);
//     const dir = path.dirname(fullPath);
//     if (!fs.existsSync(dir)) {
//         fs.mkdirSync(dir, { recursive: true });
//     }

//     // 写入 JSON 文件
//     fs.writeFile(fullPath, JSON.stringify(data, null, 4), 'utf8', (err) => {
//         if (err) {
//             console.error('保存 JSON 文件失败:', err);
//             return res.status(500).send('保存失败');
//         }
//         res.send('保存成功');
//     });
// });
// 提供静态文件
app.use('/output', express.static(path.join(__dirname, 'output')));

app.listen(port, () => {
    console.log(`服务器运行在 http://localhost:${port}`);
});