import { Alert, Checkbox, Button } from 'antd';
import { FormattedMessage, formatMessage } from 'umi-plugin-react/locale';
import React, { Component } from 'react';
import Link from 'umi/link';
import { connect } from 'dva';
import LoginComponents from './components/Login';
import styles from './style.less';
import logo from '@/assets/logo.svg';

const { Tab, UserName, Password, Mobile, Captcha, Submit } = LoginComponents;

@connect(({ login, loading }) => ({
  userLogin: login,
  submitting: loading.effects['login/login'],
}))
class Login extends Component {
  loginForm = undefined;

  constructor(props) {
    super(props)
    this.state = {
      type: 'account',
      autoLogin: true,
      codeInfo: null,
    };
    this.Timer = null;
  }

  componentWillUnmount() {
    if (this.Timer){
      clearInterval(this.Timer);
    }
  }

  changeAutoLogin = e => {
    this.setState({
      autoLogin: e.target.checked,
    });
  };

  handleSubmit = (err, values) => {
    const { type } = this.state;

    if (!err) {
      const { dispatch } = this.props;
      dispatch({
        type: 'login/login',
        payload: { ...values, type },
      });
    }
  };

  onTabChange = type => {
    this.setState({
      type,
    }, () => {
      if (type === 'qrcode') {
        this.queryGetLoginQr();
      }
    });
  };

  queryGetLoginQr = () => {
    const { dispatch } = this.props;
    dispatch({
      type: 'login/queryGetLoginQr',
    })
      .then(() => {
        const { userLogin: { codeInfo } } = this.props;
        this.setState({ codeInfo }, () => {
          this.Timer = setInterval(() => {
            this.queryGetCodeStatus()
          }, 1000);
        })
      })
  };

  queryGetCodeStatus = () => {
    const { dispatch } = this.props;
    const { userLogin: { codeInfo } } = this.props;
    dispatch({
      type: 'login/queryGetCodeStatus',
      payload: {
        loginId: codeInfo.loginId,
      },
    })
  }

  onGetCaptcha = () =>
    new Promise((resolve, reject) => {
      if (!this.loginForm) {
        return;
      }

      this.loginForm.validateFields(['mobile'], {}, async (err, values) => {
        if (err) {
          reject(err);
        } else {
          const { dispatch } = this.props;

          try {
            const success = await dispatch({
              type: 'login/getCaptcha',
              payload: values.mobile,
            });
            resolve(!!success);
          } catch (error) {
            reject(error);
          }
        }
      });
    });

  renderMessage = content => (
    <Alert
      style={{
        marginBottom: 24,
      }}
      message={content}
      type="error"
      showIcon
    />
  );

  render() {
    const { userLogin, submitting } = this.props;
    const { status, type: loginType } = userLogin;
    const { type, autoLogin, codeInfo } = this.state;
    return (
      <div className={styles.main}>
        <LoginComponents
          defaultActiveKey={type}
          onTabChange={this.onTabChange}
          onSubmit={this.handleSubmit}
          onCreate={form => {
            this.loginForm = form;
          }}
        >
          <Tab
            key="account"
            tab={formatMessage({
              id: 'user-login.login.tab-login-credentials',
            })}
          >
            {status === 'error' &&
              loginType === 'account' &&
              !submitting &&
              this.renderMessage(
                formatMessage({
                  id: 'user-login.login.message-invalid-credentials',
                }),
              )}
            <UserName
              name="userName"
              placeholder={`${formatMessage({
                id: 'user-login.login.userName',
              })}: admin or user`}
              rules={[
                {
                  required: true,
                  message: formatMessage({
                    id: 'user-login.userName.required',
                  }),
                },
              ]}
            />
            <Password
              name="password"
              placeholder={`${formatMessage({
                id: 'user-login.login.password',
              })}: ant.design`}
              rules={[
                {
                  required: true,
                  message: formatMessage({
                    id: 'user-login.password.required',
                  }),
                },
              ]}
              onPressEnter={e => {
                e.preventDefault();

                if (this.loginForm) {
                  this.loginForm.validateFields(this.handleSubmit);
                }
              }}
            />
          </Tab>
          <Tab
            key="qrcode"
            tab="二维码登录"
          >
            {status === 'error' &&
              loginType === 'qrcode' &&
              !submitting &&
              this.renderMessage(
                formatMessage({
                  id: 'user-login.login.message-invalid-verification-code',
                }),
              )}
            <div className={styles.qrcodeContainer}>
              <img alt="logo" className={styles.qrcode} src={codeInfo?codeInfo.loginCode:''} />
              <div className={styles.scanDesc}>
                <span>
                  请使用微信小程序客户端扫描二维码
                </span>
                <Button onClick={() => this.queryGetLoginQr()} icon="sync" type="link">刷新二维码</Button>
              </div>
            </div>
          </Tab>
          {type !== 'qrcode' && (
            <div>
              <Submit loading={submitting}>
                <FormattedMessage id="user-login.login.login" />
              </Submit>
            </div>
          )}
        </LoginComponents>
      </div>
    );
  }
}

export default Login;
