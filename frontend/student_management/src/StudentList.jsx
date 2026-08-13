import { useState } from "react"

function StudentList() {
    const [students, setStudents] = useState([
        { id: 1, name: "Niraj" },
        { id: 2, name: "Rahul" },
        { id: 3, name: "Sita" }
    ])
    const [name, setName] = useState("")
    return (

        <div>
            <h1 className="text-xl font-bold text-center p-10 text-blue-500 border-b-2 border-blue-500 w-full  mx-auto">Students</h1>
            <input
                className="border border-gray-400 rounded p-2 mb-4 w-full md:w-1/2"
                type="text"
                placeholder="Enter student name"
                value={name}
                onChange={(event) => setName(event.target.value)}
            />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 ">
                {students.map(student => (
                    <div className="text-lg font-bold text-left border border-gray-300 rounded-lg p-4 mb-4 w-80 " key={student.id}>
                        <h3 > {student.name} </h3>
                    </div>
                ))}
            </div>
            <div className="flex justify-center mt-4">
                <button className="bg-blue-200 hover:bg-blue-400 text-black font-bold py-2.5 px-4 rounded " onClick={() => {
                    const newStudents = [
                        ...students,
                        { id: 4, name: name }
                    ];
                    setStudents(newStudents);
                }}>Add Student</button>
            </div>
        </div>

    )
}

export default StudentList

