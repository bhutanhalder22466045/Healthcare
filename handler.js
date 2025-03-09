const nodemailer = require('nodemailer');

module.exports.sendEmail = async (event) => {
  try {
    const { receiver_email, subject, body_text } = JSON.parse(event.body);

    // Basic validation
    if (!receiver_email || !subject || !body_text) {
      return {
        statusCode: 400,
        body: JSON.stringify({ message: 'Missing required fields' }),
      };
    }

    // Configure the email transporter (Use your email credentials)
    const transporter = nodemailer.createTransport({
      service: 'gmail', // You can configure other email services
      auth: {
        user: 'official.test.mail.13@gmail.com', 
        pass: 'lpgqfawrqhxpeixc', 
      },
    });

   
    const mailOptions = {
      from: 'official.test.mail.13@gmail.com',
      to: ['bhbagh13@gmail.com'],
      subject: subject,
      text: body_text,
    };


    await transporter.sendMail(mailOptions);

    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Email sent successfully' }),
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: 'Internal server error', error: error.message }),
    };
  }
};
