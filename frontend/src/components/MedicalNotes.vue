<template>
    <div v-if="this.user.role?.name !== 'personel medyczny'" class="medical-notes">
        <div v-if="this.viewingNote" class="overlay">
            <div class="overlay-content">
                <p>{{ this.viewedNote.content }}</p>
                <br />
                <button @click="this.viewedNote = false; this.viewingNote = ''" style="background-color: red; color: white">Zamknij</button>
            </div>
        </div>
        <div v-if="this.user?.role?.name === 'pacjent'" class="patient-medical-notes">
            <table v-if="this.notes.length > 0">
                <tr>
                    <th>Lekarz prowadzący</th>
                    <th>Data utworzenia</th>
                    <th>Treść</th>
                </tr>
                <tr v-for="(note, index) in this.notes" :key="index">
                    <td>{{ note.doctor.login }}</td>
                    <td>{{ new Date(note.creation_date).toLocaleDateString() }} {{ new Date(note.creation_date).toLocaleTimeString() }}</td>
                    <td><a @click="this.viewedNote = note; this.viewingNote = true">Zobacz</a></td>
                </tr>
            </table>
            <i v-else>Obecnie nie masz żadnych notatek</i>
        </div>

        <div v-if="this.user?.role?.name === 'lekarz'" class="doctor-medical-notes">
            <router-link to="/add_note">
                <button>Dodaj notatkę</button>
            </router-link>
            <table v-if="this.notes.length > 0">
                <tr>
                    <th>Pacjent</th>
                    <th>Data utworzenia</th>
                    <th>Treść</th>
                </tr>
                <tr v-for="(note, index) in this.notes" :key="index">
                    <td>{{ note.patient.login }}</td>
                    <td>{{ new Date(note.creation_date).toLocaleDateString() }} {{ new Date(note.creation_date).toLocaleTimeString() }}</td>
                    <td><a @click="this.viewedNote = note; this.viewingNote = true">Zobacz</a></td>
                </tr>
            </table>
            <i v-else>Obecnie nie masz żadnych napisanych notatek</i>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            notes: [],
            user: {},
            viewedNote: {},
            viewingNote: false,
        }
    },
    methods: {
        loadNotes() {
            this.getRequest("notes/", (response) => {
                this.notes = response.data;
            }, () => {});
        }
    },
    mounted() {
        this.loadUser(() => {
            this.loadNotes();
        })
    }
}
</script>