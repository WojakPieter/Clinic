<template>
    <div class="start-page">
        <h2>Witaj, {{ user.login }}</h2>
        <router-link v-if="user.role?.name !== 'personel medyczny'" to="/medical_notes">
            <button>Notatki medyczne</button>
        </router-link>
        &nbsp;
        <router-link to="/visits"><button>Wizyty</button></router-link>
    </div>
</template>

<script>
export default {
    data() {
        return {
            user: {}
        }
    },
    mounted() {
        this.loadUser();
    }
}
</script>