import request from '@/utils/request';

export async function queryGetLoginQr() {
  return request(`/webApi/login/qrlogin?_t=${new Date().getTime().toString()}`);
}

export async function queryGetCaptcha() {
  return request(`/webApi/login/getCaptcha?_t=${new Date().getTime().toString()}`);
}

export async function queryGetCodeStatus(params) {
  return request('/webApi/login/getCodeStatus', {
    method: 'POST',
    data: params,
  });
}

export async function queryAccountLogin(params) {
  return request('/webApi/login/accountLogin', {
    method: 'POST',
    data: params,
  });
}
