export default function handler(request, response) {
  response.setHeader('Cache-Control', 'no-store');
  response.status(200).json({ googleMapsApiKey: process.env.HELIOS_GOOGLE_MAPS_API_KEY || '' });
}
