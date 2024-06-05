<template>
    <div class="add-note">
        <label>
            Wybierz pacjenta
            <select v-model="notePatient">
                <option v-for="(patient, index) in this.patients" :key="index" :value=patient.login>
                    {{ patient.login }}
                </option>
            </select>
        </label>
        <br />
        <label>
            Treść notatki
            <textarea v-model="noteContent">

            </textarea>
        </label>
        <br />
        <button @click="this.addNote()">Dodaj</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            noteContent: "",
            notePatient: "",
            patients: [],
            user: {}
        }
    },
    methods: {
        addNote() {
            this.putRequest("add_note/", {
                "noteContent": this.noteContent,
                "notePatient": this.notePatient
            }, () => {
                this.$router.push("/medical_notes");
            })
        }
    },
    mounted() {
        this.loadUser(() => {
            if (this.user.role.name !== "lekarz") {
                this.$router.push("/start_page");
            }
            else {
                this.loadPatients();
            }
        })
    }
}
</script>