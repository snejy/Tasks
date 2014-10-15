ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z']

def nextElement(hash, alpha)
    (alpha - hash.keys)[0]
end

def getDependencies(array, alpha)
    dependencies = {}
    arr = array.map{|e| e.chars + [""]*(array.group_by(&:size).max.last[0].size - e.size)}
    arr.transpose().each do |word|
        word.reject{ |c| c.empty? }.each do |char|
            if not dependencies.has_value?(char)
                if nextElement(dependencies,alpha)
                    dependencies[nextElement(dependencies, alpha)] = char
                else
                    false
                end
            end
        end
    end
    dependencies
end

def isSorted(array, alpha)
    h = getDependencies(array, alpha)
    if h 
        desired = []
        array.map{|e| desired.push(e.split("").
            each { |i| i.gsub!(i,h.select{|key, value| value == i }.keys.first)})}
        desired.sort == desired
    else
        false
    end
end

def main()
    puts "Number of words:"
    input = gets.chomp
    result = []

    for i in 1..input.to_i
        word = gets.chomp
        result.push(word)
    end

    if isSorted(result, ALPHABET)
        puts "YES"
        h = getDependencies(result, ALPHABET)
        replacements = ''
        ALPHABET.map {|e| h.has_key?(e) ? replacements.concat(h[e]) : replacements.concat(e)}
        puts replacements
    else
        for i in 0..1000
            currentAlphabet = ALPHABET.shuffle
            if isSorted(result, currentAlphabet)
                puts "Yes"
                h = getDependencies(result, currentAlphabet)
                replacements = ''
                currentAlphabet.map {|e| h.has_key?(e) ? 
                    replacements.concat(h[e]) : replacements.concat(e)}
                puts replacements
            end
        end
    puts "NO"
    end
end

main()
