<template>
      <div class="container mt-5">
    <h1 class="text-center">Create New Show</h1>
    <form method="POST" class="mt-4">
      <div class="form-group">
        <label for="showname">Show Name:</label>
        <input type="text" class="form-control" id="showname" name="showname" required>
      </div>
      <div class="form-group">
        <label for="rating">Rating:</label>
        <input type="number" class="form-control" id="rating" name="rating">
      </div>
      <div class="form-group">
        <label for="tags">Tags:</label>
        <input type="text" class="form-control" id="tags" name="tags">
      </div>
      <div class="form-group">
        <label for="ticketprice">Ticket Price:</label>
        <input type="number" class="form-control" id="ticketprice" name="ticketprice">
      </div>
      <div class="form-group">
        <label for="maxticket">Max Ticket:</label>
        <input type="number" class="form-control" id="maxticket" name="maxticket">
      </div>
      <button type="submit" class="btn btn-primary">Create Show</button>
    </form>
  </div>
</template>
<script>
</script>
<style scoped>
</style>