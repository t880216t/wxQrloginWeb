import { routerRedux } from 'dva/router';
import { stringify } from 'querystring';
import {
  fakeAccountLogin,
  getFakeCaptcha,
  queryGetLoginQr,
  queryGetCodeStatus,
} from '@/services/login';
import { setAuthority } from '@/utils/authority';
import { getPageQuery } from '@/utils/utils';
import route from "../../mock/route";

const Model = {
  namespace: 'login',
  state: {
    status: undefined,
    codeInfo: null,
  },
  effects: {
    *login({ payload }, { call, put }) {
      const response = yield call(fakeAccountLogin, payload);
      yield put({
        type: 'changeLoginStatus',
        payload: response,
      }); // Login successfully

      if (response.status === 'ok') {
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
    },

    *getCaptcha({ payload }, { call }) {
      yield call(getFakeCaptcha, payload);
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
      yield put({ type: 'changeLoginStatus', payload: { status: 'err', currentAuthority: 'guest' } });
      const res = yield call(queryGetCodeStatus, payload);
      if (res && res.code === 0) {
        yield put({ type: 'changeLoginStatus', payload: { status: 'ok', currentAuthority: 'admin' } });
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
    },
  },
  reducers: {
    changeLoginStatus(state, { payload }) {
      setAuthority(payload.currentAuthority);
      return {
        ...state,
        status: payload.status,
        // type: payload.type,
      };
    },
    updateState(state, { payload }) {
      return { ...state, ...payload }
    },
  },
};
export default Model;
