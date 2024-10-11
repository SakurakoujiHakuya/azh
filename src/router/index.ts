import { createRouter, createWebHistory } from 'vue-router';
import Analyze from '../view/Analyze.vue';
import Decrypt from '../view/Decrypt.vue';
import Diagnosis from '../view/Diagnosis.vue';
import Encipher from '../view/Encipher.vue';
import Security from '../view/Security.vue';
import Setting from '../view/Setting.vue';

const routes = [
    {
        path: '/',
        redirect: '/analyze' // 设置默认路由
    },
    {
        path: '/analyze',
        component: Analyze
    },
    {
        path: '/decrypt',
        component: Decrypt
    },
    {
        path: '/diagnosis',
        component: Diagnosis
    },
    {
        path: '/encipher',
        component: Encipher
    },
    {
        path: '/security',
        component: Security
    },
    {
        path: '/setting',
        component: Setting
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;