<template>
    <div class="logging-screen">
        <p style="color: red" v-if="this.errorMessage">{{ this.errorMessage }}</p>
        <label>
            Login:
            <input v-model="login">
        </label>
        <br />
        <label>
            Hasło:
            <input v-model="password" type="password">
        </label>
        <br /><br />
        <button @click="this.logIn()">Zaloguj się</button>
        <p>Nie masz konta?</p>
        <router-link to="/register">
            <button>Zarejestruj się</button>
        </router-link>
    </div>
</template>

<script>
export default {
    data() {
        return {
            errorMessage: "",
            login: "",
            password: ""
        }
    },
    methods: {
        logIn() {
            if (!this.login || !this.password) {
                this.errorMessage = "Należy podać dane logowania";
            }
            else {
                this.postRequest("login/", {
                    login: this.login,
                    password: this.password
                }, (response) => {
                    window.localStorage.setItem('token', response.data);
                    this.$router.push("/start_page");
                }, (error) => {
                    this.errorMessage = "Nieprawidłowe dane";
                })
            }
        }
    },
}
</script>