import { createApp } from 'vue'
import { createWebHistory, createRouter } from "vue-router";
import './style.css'
import App from './App.vue'
import VueAxios from "vue-axios"
import VueCookies from "vue-cookies"
import axios from "axios"
import VIdle from "v-idle"
import LoggingScreen from "./components/LoggingScreen.vue"
import RegisterScreen from "./components/RegisterScreen.vue"
import StartPage from "./components/StartPage.vue"
import MedicalNotes from "./components/MedicalNotes.vue"
import AddNote from "./components/AddNote.vue"
import Visits from "./components/Visits.vue"
import AddVisit from "./components/AddVisit.vue"

const routes = [
    { path: '/', component: LoggingScreen },
    { path: '/register', component: RegisterScreen },
    { path: '/start_page', component: StartPage },
    { path: '/medical_notes', component: MedicalNotes },
    { path: '/add_note', component: AddNote },
    { path: '/visits', component: Visits },
    { path: '/add_visit', component: AddVisit },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

const app = createApp(App);
axios.interceptors.request.use(
    function(config) {
        // Do something before request is sent
        config.withCredentials = true;
        return config;
    },
    function(error) {
        // Do something with request error
        return Promise.reject(error);
    }
);
app.provide("axios", app.config.globalProperties.axios);
app.use(VueAxios, axios);
app.use(VueCookies);
app.use(VIdle);
app.use(router);
app.mixin({
    data() {
        return {
            patients: [],
            requestProcessing: false,
            user: {}
        }
    },
    methods: {
        getRequest(url, _thenHandler, _catchHandler = () => {}) {
            const headers = {
                accept: "application/json",
                Authorization: "Bearer " + window.localStorage.getItem("token"),
            };
            this.requestProcessing = true;
            this.axios
                .get('http://127.0.0.1:8000/' + url, { headers })
                .then((response) => {
                    this.requestProcessing = false;
                    _thenHandler(response);
                })
                .catch((error) => {
                    this.requestProcessing = false;
                    if (error.response.data && error.response.data.message == "JWT Token expired") {
                        this.refreshToken(() => {
                            this.getRequest(url, _thenHandler, _catchHandler);
                        })
                    }
                    else {
                        _catchHandler(error);
                    }
                    
                });
        },
        postRequest(url, data, _thenHandler, _catchHandler = () => {}) {
            const headers = {
                accept: "application/json",
                Authorization: "Bearer " + window.localStorage.getItem("token"),
                
            };
            this.requestProcessing = true;
            this.axios
                .post('http://127.0.0.1:8000/' + url, data, { headers })
                .then((response) => {
                    this.requestProcessing = false;
                    _thenHandler(response);
                })
                .catch((error) => {
                    this.requestProcessing = false;
                    if (error.response.data && error.response.data.message == "JWT Token expired") {
                        this.refreshToken(() => {
                            this.postRequest(url, data, _thenHandler, _catchHandler);
                        })
                    }
                    else {
                        _catchHandler(error);
                    }
                });
        },
        putRequest(url, data, _thenHandler, _catchHandler = () => {}) {
            const headers = {
                accept: "application/json",
                Authorization: "Bearer " + window.localStorage.getItem("token"),
            };
            this.requestProcessing = true;
            this.axios
                .put('http://127.0.0.1:8000/' + url, data, { headers })
                .then((response) => {
                    this.requestProcessing = false;
                    _thenHandler(response);
                })
                .catch((error) => {
                    this.requestProcessing = false;
                    if (error.response.data && error.response.data.message == "JWT Token expired") {
                        this.refreshToken(() => {
                            this.putRequest(url, data, _thenHandler, _catchHandler);
                        })
                    }
                    else {
                        _catchHandler(error);
                    }
                });
        },
        deleteRequest(url, _thenHandler, _catchHandler = () => {}) {
            const headers = {
                accept: "application/json",
                Authorization: "Bearer " + window.localStorage.getItem("token"),
            };
            this.requestProcessing = true;
            this.axios
                .delete('http://127.0.0.1:8000/' + url, { headers })
                .then((response) => {
                    this.requestProcessing = false;
                    _thenHandler(response);
                })
                .catch((error) => {
                    this.requestProcessing = false;
                    if (error.response.data && error.response.data.message == "JWT Token expired") {
                        this.refreshToken(() => {
                            this.deleteRequest(url, _thenHandler, _catchHandler);
                        })
                    }
                    else {
                        _catchHandler(error);
                    }
                });
        },
        refreshToken(_callback = () => {}) {
            const headers = {
                accept: "application/json"
            };
            this.axios
                .post('http://127.0.0.1:8000/refresh_token/', { headers })
                .then((response) => {
                    window.localStorage.setItem("token", response.data);
                    _callback()
                })
                .catch(() => {
                    window.localStorage.removeItem("token");
                    this.$router.push("/");
                })
        },
        loadUser(_callback = () => {}) {
            this.getRequest("user/", (response) => {
                this.user = response.data;
                _callback();
            }, (error) => {
                this.$router.push("/");
            }) 
        },
        loadPatients(_callback = () => {}) {
            this.getRequest("patients/", (response) => {
                this.patients = response.data;
                _callback();
            })
        },
        logout(_callback = () => {}) {
            this.postRequest("logout/", {}, () => {
                window.localStorage.removeItem("token");
                this.$router.push("/");
            })
        }
    },
    watch: {
        requestProcessing(newOne) {
            setTimeout(() => {
              const btns = document.querySelectorAll("button");
              if (newOne) {
                for (let btn of btns) {
                  if (btn.disabled) {
                    btn.classList.add("default-disabled");
                  }
                  btn.disabled = true;
                }
              } else {
                for (let btn of btns) {
                  if (!btn.classList.contains("default-disabled")) {
                    btn.disabled = false;
                  }
                  else {
                    btn.classList.remove("default-disabled");
                  }
                }
              }
            }, 300)
        }
    }
})
app.mount('#app');
