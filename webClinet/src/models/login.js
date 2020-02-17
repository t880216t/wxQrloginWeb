import { routerRedux } from 'dva/router';
import { stringify } from 'querystring';
import { message } from 'antd'
import {
  fakeAccountLogin,
  queryGetCaptcha,
  queryAccountLogin,
  queryGetLoginQr,
  queryGetCodeStatus,
} from '@/services/login';
import { setAuthority } from '@/utils/authority';
import { getPageQuery } from '@/utils/utils';

const Model = {
  namespace: 'login',
  state: {
    status: undefined,
    codeInfo: null,
    captchCode: null,
  },
  effects: {
    *login({ payload }, { call, put }) {
      const response = yield call(queryAccountLogin, payload);
      if (response && response.code === 0) {
        yield put({ type: 'changeLoginStatus', payload: { status: 'ok', currentAuthority: response.currentAuthority } });
        const urlParams = new URL(window.location.href);
        const params = getPageQuery();
        let { redirect } = params;

        if (redirect) {
          const redirectUrlParams = new URL(redirect);

          if (redirectUrlParams.origin === urlParams.origin) {
            redirect = redirect.substr(urlParams.origin.length);

            if (redirect.match(/^\/.*#/)) {
              redirect = redirect.substr(redirect.indexOf('#') + 1);
            }
          } else {
            window.location.href = '/';
            return;
          }
        }

        yield put(routerRedux.replace(redirect || '/'));
      }
      if (response && response.code !== 0) {
        yield put({ type: 'changeLoginStatus', payload: { status: 'err', currentAuthority: 'guest' } });
        message.error(response.msg)
      }
    },

    *queryGetCaptcha({ payload }, { call, put }) {
      const response = yield call(queryGetCaptcha, payload);
      if (response) {
        yield put({ type: 'updateState', payload: { captchCode: response.content.captchCode } });
      }
    },

    *logout(_, { put }) {
      const { redirect } = getPageQuery(); // redirect

      if (window.location.pathname !== '/user/login' && !redirect) {
        yield put(
          routerRedux.replace({
            pathname: '/user/login',
            search: stringify({
              redirect: window.location.href,
            }),
          }),
        );
      }
    },

    *queryGetLoginQr({ payload }, { call, put }) {
      yield put({ type: 'updateState', payload: { loginCode: null } });
      const res = yield call(queryGetLoginQr, payload);
      if (res) {
        yield put({ type: 'updateState', payload: { codeInfo: res.content } });
      }
    },

    *queryGetCodeStatus({ payload }, { call, put }) {
      const res = yield call(queryGetCodeStatus, payload);
      if (res && res.code === 0) {
        // yield put({ type: 'changeLoginStatus', payload: { status: 'ok', currentAuthority: 'admin' } });
        const urlParams = new URL(window.location.href);
        const params = getPageQuery();
        let { redirect } = params;
        if (redirect) {
          const redirectUrlParams = new URL(redirect);
          if (redirectUrlParams.origin === urlParams.origin) {
            redirect = redirect.substr(urlParams.origin.length);
            if (redirect.match(/^\/.*#/)) {
              redirect = redirect.substr(redirect.indexOf('#') + 1);
            }
          } else {
            window.location.href = '/';
            return;
          }
        }
        yield put(routerRedux.replace(redirect || '/'));
      }
      if (res && res.code === 10003) {
        // yield put({ type: 'changeLoginStatus', payload: { status: 'err', currentAuthority: 'guest' } });
        message.error(res.msg)
      }
    },
  },
  reducers: {
    changeLoginStatus(state, { payload }) {
      setAuthority(payload.currentAuthority);
      return {
        ...state,
        status: payload.status,
      };
    },
    updateState(state, { payload }) {
      return { ...state, ...payload }
    },
  },
};
export default Model;
