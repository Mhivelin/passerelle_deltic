using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace appPasserelleDELTIC
{
    public partial class LoginForm : Form
    {
        public LoginForm()
        {
            InitializeComponent();
        }

        private void LoginForm_Load(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private async void loginButton_Click(object sender, EventArgs e)
        {
            ApiService apiService = new ApiService();
            string token = await apiService.LoginAsync(usernameTextBox.Text, passwordTextBox.Text);
            if (!string.IsNullOrEmpty(token))
            {
                MainForm mainForm = new MainForm(token);
                mainForm.Show();
                this.Hide();
            }
            else
            {
                MessageBox.Show("Échec de la connexion. Veuillez vérifier vos identifiants.");
            }
        }




        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void passwordTextBox_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
