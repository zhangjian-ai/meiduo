import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import api from './api'

import VueWechatTitle from "vue-wechat-title";
import ElementUI from 'element-ui';
import { MessageBox, Message } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';

import axios from 'axios'

//环境的切换
if (process.env.NODE_ENV == 'development') {
    axios.defaults.baseURL = 'http://www.meiduo.site:8000/';
}
if (process.env.NODE_ENV == 'production') {
    axios.defaults.baseURL = 'http://121.4.47.229:8000/';
}

// 默认携带cookie发起请求和保存cookie
axios.defaults.withCredentials = true

// http request 拦截器
axios.interceptors.request.use(
    config => {
        if (store.state.token) {  // 判断是否存在token，如果存在的话，则每个http header都加上token。本项目使用JWT
            config.headers.Authorization = `JWT ${store.state.token}`;
        }
        return config;
    },
    err => {
        return Promise.reject(err);
    });

// http response 拦截器
axios.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        let res = error.response
        if (res) {
            switch (res.status) {
                case 401:
                    MessageBox.confirm(
                        '您的登录信息已过期，您可以取消以停留在此页，或重新登录',
                        '系统提示',
                        {
                            confirmButtonText: '重新登录',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }
                    )
                        .then(() => {
                            // 返回 401 清除token信息并跳转到登录页面
                            store.commit('setStatus');
                            router.replace({
                                name: 'login',
                                query: { redirect: router.currentRoute.fullPath }  // 登陆之后再回到当前页面
                            })
                        })
                        .catch(() => {
                            store.commit('setStatus');
                            router.go(0);  // 刷新一下当前页面
                        })
                    break;
                case 400:
                    Message({
                        message: res.data.msg || '客户端错误',
                        type: 'error',
                    })
                    break;

                case 403:
                    Message({
                        message: res.data.msg || '您的权限不足',
                        type: 'error',
                    })
                    break;

                case 404:
                    Message({
                        message: res.data.msg || '网络请求不存在',
                        type: 'error',
                    })
                    break;

                case 500:
                    Message({
                        message: res.data.msg || '服务器异常',
                        type: 'error',
                    })
                    break;

                case 501:
                    Message({
                        message: res.data.msg || '您的操作被取消或不允许提交',
                        type: 'warning',
                    })
                    break;

                default:
                    Message({
                        message: res.data.msg || '服务器正在开小差...',
                        type: 'error',
                    })
            }
        }
        // return Promise.reject(error.response.data)   // 返回接口返回的错误信息
        return Promise.reject(error.response)   // 返回接口返回的错误信息

    });

Vue.prototype.$axios = axios;    //全局注册，使用方法为:this.$axios
Vue.prototype.$api = api;    //全局注册，使用方法为:this.$api  api封装统一管理


//  路由权限判断
router.beforeEach((to, from, next) => {
    if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
        if (store.state.token) {  // 通过vuex state获取当前的token是否存在
            next();
        }
        else {

            next({
                name: 'login',
                query: { redirect: to.fullPath }  // 将跳转的路由path作为参数，登录成功后跳转到该路由
            })
        }
    }
    else {
        next();
    }
})

Vue.config.productionTip = false

Vue.use(ElementUI);
Vue.use(VueWechatTitle);


new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
