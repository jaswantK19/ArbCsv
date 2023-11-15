import LoginForm from './components/LoginForm'
import RegistrationForm from './components/RegistrationForm'
import MainDashboard from './components/MainDashboard'

export default [
    {
        path:"/login",
        component: LoginForm,
    },
    {
        path: "/",
        component: RegistrationForm
    },
    {
        path:'/register',
        component: RegistrationForm
    },
    {
        path: "/dashboard",
        component: MainDashboard 
    }
]