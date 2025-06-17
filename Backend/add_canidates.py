from models import Candidate
from pymongo import MongoClient


#{
#     id: 1,
#     name: 'Bachir Ammar',
#     role: 'Software Engineer',
#     photo: "https://images.unsplash.com/photo-1607990281513-2c110a25bd8c?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdulloh&backgroundColor=39484f&mouth=smile&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Software Engineer',
#         years: '4+ years'
#       }
#     ],
#     about: 'Experienced software engineer with expertise in full-stack development, focusing on React, Node.js, and cloud technologies. Strong problem-solving skills and experience in building scalable applications.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['React', 'Node.js', 'JavaScript', 'Python', 'MongoDB'],
#     cvPath: bachirCV
#   },
#   {
#     id: 2,
#     name: 'Sumaiya Fathima',
#     role: 'Software Developer | Instrumentation Engineer',
#     photo: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Sumaiya&backgroundColor=39484f&mouth=smile&gender=female&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Software Developer',
#         years: '2+ years'
#       }
#     ],
#     about: 'Software Developer with a background in Instrumentation Engineering. Experienced in building responsive web applications and working with modern JavaScript frameworks.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['React', 'JavaScript', 'HTML/CSS', 'Python', 'SQL'],
#     cvPath: sumaiyaCV
#   },
#   {
#     id: 3,
#     name: 'Obada Outabachi',
#     role: 'Full Stack Developer',
#     photo: "https://images.unsplash.com/photo-1562788869-4ed32648eb72?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdulloh&backgroundColor=39484f&mouth=smile&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Full Stack Developer',
#         years: '3+ years'
#       }
#     ],
#     about: 'Full Stack Developer with strong expertise in modern web technologies. Experienced in building end-to-end applications using React and Node.js ecosystem.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['React', 'Node.js', 'JavaScript', 'TypeScript', 'PostgreSQL'],
#     cvPath: obadaCV
#   },
#   {
#     id: 4,
#     name: 'Abdulloh Rashidov',
#     role: 'Frontend Developer',
#     photo: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdulloh&backgroundColor=39484f&mouth=smile&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Frontend Developer',
#         years: '2+ years'
#       }
#     ],
#     about: 'Frontend Developer with expertise in React and modern JavaScript frameworks. Experienced in building responsive and user-friendly web applications.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['React', 'JavaScript', 'HTML/CSS', 'TypeScript', 'Redux'],
#     cvPath: abdullohCV
#   },
#   {
#     id: 5,
#     name: 'Abdullah Ghazi',
#     role: 'Software Engineer',
#     photo: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdulloh&backgroundColor=39484f&mouth=smile&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Software Engineer',
#         years: '3+ years'
#       }
#     ],
#     about: 'Software Engineer with strong background in full-stack development. Experienced in building scalable applications and working with modern technologies.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['JavaScript', 'Python', 'React', 'Node.js', 'SQL'],
#     cvPath: abdullahCV
#   },
#   {
#     id: 6,
#     name: 'Amina Alnaqbi',
#     role: 'Software Developer',
#     photo: "https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Sumaiya&backgroundColor=39484f&mouth=smile&gender=female&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Software Developer',
#         years: '2+ years'
#       }
#     ],
#     about: 'Software Developer with experience in web development and application design. Strong problem-solving skills and attention to detail.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['Java', 'JavaScript', 'React', 'SQL', 'HTML/CSS'],
#     cvPath: aminaCV
#   },
#   {
#     id: 7,
#     name: 'Syimyk Zhakypov',
#     role: 'Full Stack Developer',
#     photo: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdulloh&backgroundColor=39484f&mouth=smile&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Full Stack Developer',
#         years: '3+ years'
#       }
#     ],
#     about: 'Full Stack Developer with expertise in both frontend and backend development. Experienced in building complete web applications from scratch.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['React', 'Node.js', 'MongoDB', 'JavaScript', 'Python'],
#     cvPath: syimykCV
#   },
#   {
#     id: 8,
#     name: 'Mariam Kovoor',
#     role: 'Software Engineer',
#     photo: "https://images.unsplash.com/photo-1598550880863-4e8aa3d0edb4?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Sumaiya&backgroundColor=39484f&mouth=smile&gender=female&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Software Engineer',
#         years: '2+ years'
#       }
#     ],
#     about: 'Software Engineer with focus on web development and cloud technologies. Strong analytical skills and experience in agile development.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['JavaScript', 'React', 'AWS', 'Node.js', 'Python'],
#     cvPath: mariamCV
#   },
#   {
#     id: 9,
#     name: 'Alexandra Ball',
#     role: 'Frontend Developer',
#     photo: "https://images.unsplash.com/photo-1580894732930-0baebb5d1414?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdulloh&backgroundColor=39484f&mouth=smile&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Frontend Developer',
#         years: '3+ years'
#       }
#     ],
#     about: 'Frontend Developer specializing in creating responsive and intuitive user interfaces. Experienced in modern JavaScript frameworks and UI/UX principles.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['React', 'JavaScript', 'HTML/CSS', 'Vue.js', 'UI/UX'],
#     cvPath: alexandraCV
#   },
#   {
#     id: 10,
#     name: 'Mustafa Radwan',
#     role: 'Full Stack Developer',
#     photo: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=400",
#     photoBack: "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdulloh&backgroundColor=39484f&mouth=smile&style=circle",
#     experience: [
#       {
#         company: 'Previous Companies',
#         position: 'Full Stack Developer',
#         years: '4+ years'
#       }
#     ],
#     about: 'Full Stack Developer with extensive experience in web development. Skilled in both frontend and backend technologies with a focus on scalable solutions.',
#     location: 'Abu Dhabi, UAE',
#     skills: ['React', 'Node.js', 'JavaScript', 'Python', 'MongoDB'],
#     cvPath: mustafaCV
#   }

# Backend/media/Abdullah Ghazi_CV.pdf
# Backend/media/Abdulloh Rashidov_CV.pdf
# Backend/media/Ahmed Hassan_CV.pdf
# Backend/media/Ahmed_Salem_CV.pdf
# Backend/media/Alexander_Derugo_CV.pdf
# Backend/media/Alexandra_Ball_CV.pdf
# Backend/media/Amina_Alnaqbi_CV.pdf
# Backend/media/Ammar Albreiki_CV.pdf
# Backend/media/Anas Ajaanan_CV.pdf
# Backend/media/Bachir_Ammar_CV.pdf
# Backend/media/Cristina Cestini_CV.pdf
# Backend/media/Ilia_MAZOURINE_CV.pdf
# Backend/media/Imran_Mustafa_CV.pdf
# Backend/media/Jinxiu Yao_CV.pdf
# Backend/media/Lara Elkhoury CV.pdf
# Backend/media/Mariam Kovoor_CV.pdf
# Backend/media/Mehrin Firdousi_CV.pdf
# Backend/media/Mohammed Ehsan CV.pdf
# Backend/media/Mustafa Radwan_CV.pdf
# Backend/media/Nousheen_Ali_CV.pdf
# Backend/media/Obada_Outabachi_CV.pdf
# Backend/media/Oguz utku Aydemir_CV.pdf
# Backend/media/Omar ElGhamry_CV.pdf
# Backend/media/Raj_Rangwani_CV.pdf
# Backend/media/ShamaAlmazrouei_CV.pdf
# Backend/media/Sumaiya Fathima_CV.pdf
# Backend/media/Syimyk Zhakypov_CV.pdf
# Backend/media/WillemSmith_CV.pdf


def add_candidate(MONGO_DB: MongoClient):
    if MONGO_DB["candidates"].count_documents({}) > 0:
        return
    l = []
    l.append(Candidate(name="Bachir Ammar", email="bachir@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=4, specialization="Full Stack Developer", DOB="1990-01-01", skills=["React", "Node.js", "JavaScript", "Python", "MongoDB"], CVPath="media/Bachir_Ammar_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Sumaiya Fathima", email="sumaiya@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=2, specialization="Software Developer", DOB="1990-01-01", skills=["React", "JavaScript", "HTML/CSS", "Python", "SQL"], CVPath="media/Sumaiya_Fathima_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Obada Outabachi", email="obada@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=3, specialization="Full Stack Developer", DOB="1990-01-01", skills=["React", "Node.js", "JavaScript", "TypeScript", "PostgreSQL"], CVPath="media/Obada_Outabachi_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Abdulloh Rashidov", email="abdulloh@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=2, specialization="Frontend Developer", DOB="1990-01-01", skills=["React", "JavaScript", "HTML/CSS", "TypeScript", "Redux"], CVPath="media/Abdulloh_Rashidov_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Abdullah Rashidov", email="abdullah@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=3, specialization="Software Engineer", DOB="1990-01-01", skills=["JavaScript", "Python", "React", "Node.js", "SQL"], CVPath="media/Abdullah_Rashidov_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Amina Alnqbi", email="amina@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=2, specialization="Software Developer", DOB="1990-01-01", skills=["Java", "JavaScript", "React", "SQL", "HTML/CSS"], CVPath="media/Amina_Alnaqbi_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Syimyk Zhakypov", email="syimyk@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=3, specialization="Full Stack Developer", DOB="1990-01-01", skills=["React", "Node.js", "JavaScript", "TypeScript", "PostgreSQL"], CVPath="media/Syimyk Zhakypov_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Mariam Kovoor", email="mariam@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=2, specialization="Software Engineer", DOB="1990-01-01", skills=["JavaScript", "Python", "React", "Node.js", "SQL"], CVPath="media/Mariam_Kovoor_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Alexandra Ball", email="alexandra@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=3, specialization="Frontend Developer", DOB="1990-01-01", skills=["React", "JavaScript", "HTML/CSS", "TypeScript", "Redux"], CVPath="media/Alexandra_Ball_CV.pdf", Photo="", PhotoBack=""))
    l.append(Candidate(name="Mustafa Radwan", email="mustafa@gmail.com", nationality="UAE", phone="1234567890", education="Master's", years_of_experience=4, specialization="Full Stack Developer", DOB="1990-01-01", skills=["React", "Node.js", "JavaScript", "TypeScript", "PostgreSQL"], CVPath="media/Mustafa_Radwan_CV.pdf", Photo="", PhotoBack=""))

    for i in l:
        MONGO_DB["candidates"].insert_one(i.dict())
    
    return "Candidates added successfully"