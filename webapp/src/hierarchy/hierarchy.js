// eslint-disable-next-line no-unused-vars
function dfsHierarchy(hierarchy, alreadyPresent, res) {

    if (hierarchy.children) {
        hierarchy.children.forEach(el => {
            dfsHierarchy(el, alreadyPresent, res)
        })
    }


    alreadyPresent.forEach(el => {
            if (Array.isArray(hierarchy.content) && hierarchy.content.includes(el)) {
                res.push(hierarchy.content)
            }
        }
    )
}

function getRecommendation(hierarchy, alreadyPresent) {
    let result = {}

    alreadyPresent.forEach(el => {
        const res = []
        dfsHierarchy(hierarchy.payload, [el], res)

        const set = new Set()
        res.forEach(el => el.forEach(tag => set.add(tag)))

        result[el] = [...set]
    })

    const finalSet = new Set()

    for (let i = 0; i < result[alreadyPresent[0]].length; i++) {
        for (let j = 0; j < Object.keys(result).length; j++)
            finalSet.add(result[alreadyPresent[j]][i])
    }


    return [...finalSet]


}


export {
    getRecommendation
}


