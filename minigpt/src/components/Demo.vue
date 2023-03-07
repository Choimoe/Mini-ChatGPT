<template>
  <div>
  <h1>ChatBot Admin Panel</h1>
  <label for="question">Question:</label>
  <input type="text" id="question"><br>
  <label for="answer">Answer:</label>
  <input type="text" id="answer"><br>
  <label for="keyword">Keyword:</label>
  <input type="text" id="keyword"><br>
  <label for="delete_id">Delete ID:</label>
  <input type="text" id="delete_id"><br>
  <button id="search_btn">Search</button>
  <button id="add_btn">Add</button>
  <button id="update_btn">Update</button>
  <button id="delete_btn">Delete</button>

  <table id="result_table">
    <thead>
    <tr>
      <th>ID</th>
      <th>Question</th>
      <th>Answer</th>
    </tr>
    </thead>
    <tbody>
    </tbody>
  </table>
  <script src="https://cdn.jsdelivr.net/npm/vue"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
  <script src="app.js"></script>
  </div>
</template>

<script>
var app = new Vue({
  el: '#app',
  data: {
    questions: [],
    keyword: '',
    newQuestion: '',
    newAnswer: '',
    deleteId: ''
  },
  mounted: function() {
    this.search();
  },
  methods: {
    search: function() {
      axios.get('/search', {
        params: {
          keyword: this.keyword
        }
      })
          .then(function(response) {
            app.questions = response.data;
          })
          .catch(function(error) {
            console.log(error);
          });
    },
    add: function() {
      axios.post('/add', {
        question: this.newQuestion,
        answer: this.newAnswer
      })
          .then(function(response) {
            app.questions.push(response.data);
            app.newQuestion = '';
            app.newAnswer = '';
          })
          .catch(function(error) {
            console.log(error);
          });
    },
    update: function(id, question, answer) {
      axios.put('/update', {
        id: id,
        question: question,
        answer: answer
      })
          .then(function(response) {
            console.log(response);
          })
          .catch(function(error) {
            console.log(error);
          });
    },
    remove: function(id) {
      axios.delete('/delete/' + id)
          .then(function(response) {
            console.log(response);
            app.search();
          })
          .catch(function(error) {
            console.log(error);
          });
    }
  }
});

</script>

<style scoped>

</style>