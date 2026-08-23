function StudentCard() {
    return (
                    <div className="text-lg font-bold text-left border border-gray-300 rounded-lg p-4 mb-4 w-80 " key={student.id}>
                        <h3 > {student.name} </h3>
                    </div>
    )
}

export default StudentCard