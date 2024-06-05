<template>
    <div class="add-visit">
        <p style="color: red" v-if="this.errorMessage">{{ this.errorMessage }}</p>
        <label>
            Wybierz lekarza:
            <select v-model="visitDoctor">
                <option v-for="(doctor, index) in this.doctors" :key="index">
                    {{ doctor.login }}
                </option>
            </select>
        </label>
        <br />
        Wybierz datę:
        <input v-model="visitDate" type="date">
        &nbsp;godz. &nbsp;
        <select v-model="visitHour">
            <option>8</option>
            <option>9</option>
            <option>10</option>
            <option>11</option>
            <option>12</option>
            <option>13</option>
            <option>14</option>
            <option>15</option>
            <option>16</option>
        </select>
        <br />
        <button @click="this.addVisit()">Zatwierdź</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            doctors: [],
            errorMessage: "",
            visitDate: "",
            visitDoctor: "",
            visitHour: 8
        }
    },
    methods: {
        addVisit() {
            this.putRequest("visits/", {
                visitDoctor: this.visitDoctor,
                hour: this.visitHour,
                date: this.visitDate
            }, () => {
                this.$router.push("/visits"); 
            }, (error) => {
                this.errorMessage = error?.response?.data?.message;
            })
        },
        loadDoctors() {
            this.getRequest(
                "doctors/", 
                (response) => {this.doctors = response.data}, 
                () => {}
            );
        }
    },
    mounted() {
        this.loadDoctors();
    }
}
</script>