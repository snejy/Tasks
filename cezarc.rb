ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z']

def nextElement(hash, alpha)
    (alpha - hash.keys)[0]
end

def getDependencies(array, alpha)
    dependencies = Hash.new()
    arr = array.map{|e| e.chars + [""]*(array.group_by(&:size).max.last[0].size - e.size)}
    for word in arr.transpose()
        for char in word.reject{ |c| c.empty? }
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
        for i in 0..1000 #tries with 1000 different permutations of ALPHABET ... with more than 1000 gets slower
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
