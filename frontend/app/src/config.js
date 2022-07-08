//import runtimeEnv from '@mars/heroku-js-runtime-env';

//const env = runtimeEnv();
const config = {
  apiBasePath: 'http://127.0.0.1:8002', // env.REACT_APP_API_BASE_PATH ||
  reactAppMode: 'dev', // process.env.REACT_APP_MODE ||
};

export default config;
