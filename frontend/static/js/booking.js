// frontend/js/booking.js
async function bookRepair() {
  // Get location, breakdown type, etc.
  const booking = {
    /* data */
  };
  await apiCall("/bookings/", "POST", booking);
  // Handle response
}

async function bookTowing() {
  // Similar
}
