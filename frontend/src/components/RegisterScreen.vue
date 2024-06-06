<template>
    <div class="register-screen">
        <p style="color: red" v-if="this.errorMessage">{{ this.errorMessage }}</p>
        <label>
            Login:
            <input v-model="login">
        </label>
        <br />
        <label>
            Hasło:
            <input type="password" v-model="password">
        </label>
        <br />
        <label>
            Powtórz hasło:
            <input type="password" v-model="repeatPassword">
        </label>
        <br />
        <label>
            Rola:
            <select v-model="role">
                <option>lekarz</option>
                <option>pacjent</option>
                <option>personel medyczny</option>
            </select>
        </label>
        <br />
        <button @click="this.register()">Załóż konto</button>
        <br />
        <div v-if="this.registerSuccessful">
            <p style="color: green">Konto utworzone</p>
            <router-link to="/">
                <button>Zaloguj się</button>
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            errorMessage: "",
            login: "",
            password: "",
            registerSuccessful: false,
            repeatPassword: "",
            role: ""
        }
    },
    methods: {
        register() {
            if (this.password !== this.repeatPassword) {
                this.errorMessage = "Hasła nie są takie same";
                return;
            }
            this.postRequest("register/", {
                login: this.login,
                password: this.password,
                role: this.role
            }, () => {
                this.registerSuccessful = true;
                this.errorMessage = "";
            }, (error) => {
                if (error.response && error.response && error.response.data && error.response.data.message) {
                    this.errorMessage = error.response.data.message;
                }
                if (error.response.status == 500) {
                    this.errorMessage = "Błąd serwera";
                }
            })

        }
    }
}
</script>