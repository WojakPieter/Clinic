<template>
    <div class="header">
        <p>Witaj <span id="user-login"></span></p>
        <router-link to="/start_page"><button>Strona główna</button></router-link>
        <button @click="this.logout()">Wyloguj się</button>
    </div>
</template>

<style scoped>
.header {
    height: 60px;
    background-color: black;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}

p {
    color: white;
}

button {
    height: 40px;
}
</style>