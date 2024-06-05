<template>
    <div class="visits">
        <p style="color: red" v-if="this.errorMessage">{{ this.errorMessage }}</p>
        <div class="patient-visits">
            <router-link to="/add_visit">
                <button>Umów się</button>
            </router-link>
            <br />
            <table v-if="this.visits.length">
                <tr>
                    <th v-if="this.user?.role?.name === 'pacjent'">Lekarz</th>
                    <th v-if="this.user?.role?.name === 'lekarz'">Pacjent</th>
                    <th>Data</th>
                    <th></th>
                </tr>
                <tr v-for="(visit, index) in this.visits" :key="index">
                    <td v-if="this.user?.role?.name !== 'lekarz'">{{ visit.doctor.login }}</td>
                    <td v-if="this.user?.role?.name !== 'pacjent'">{{ visit.patient.login }}</td>
                    <td>{{ visit.date }} godz. {{ visit.hour }}</td>
                    <td><button @click="this.cancelVisit(visit.id)">Anuluj</button></td>
                </tr>
            </table>
            <i v-else>Brak wizyt</i>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            errorMessage: "",
            user: {},
            visits: []
        }
    },
    methods: {
        cancelVisit(id) {
            this.deleteRequest("visit/" + id, () => {
                this.loadVisits();
            }, (error) => {
                this.errorMessage = error?.response?.data?.message;
            })
        },
        loadVisits() {
            this.getRequest(
                "visits/", (response) => {
                    this.visits = response.data;
                }, () => {}
            );
        },
    },
    mounted() {
        this.loadUser(() => {
            this.loadVisits();
        })
    }
}
</script>