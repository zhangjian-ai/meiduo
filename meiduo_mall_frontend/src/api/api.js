import axios from 'axios'


// 检查是否勾选规格
export const check_spec = (specs, origin_specs) => {
    let res = false;
    if (specs.length != origin_specs.length) {
        res = true;
    } else {
        specs.forEach(value => {
            if (typeof value != 'string') {
                res = true;
            }
        });
    }
    return res;
}

// 查询用户收货地址
export const address = () => { return axios.get('address/'); }

// 预保存需要生成订单的sku
export const selects = params => {return axios.post('selects/',params)}

// 查询待结算商品列表
export const order_settlement_list = () => {return axios.get('orders/settlement/')}

// 提交订单
export const submit_order = params => {return axios.post('orders/submit/',params)}

// 获取支付包三方支付地址
export const payment_url = params => {return axios.get('order/payment/' + params + '/')}

// 支付宝支付后验证
export const verify_alipay = params => {return axios.put('order/verify/?' + params)}

// 获取订单列表
export const orders = data => {return axios.get('orders/list/', {params: data})}

// 获取单条订单信息
export const order = params => {return axios.get('orders/retrieve/' + params + '/')}

// 搜索商品
export const search = data => {return axios.get('skus/search/', {params: data})}
