#https://www.freecodecamp.org/news/develop-database-driven-web-apps-with-python-flask-and-mysql/


from flask import Flask, render_template
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def plot():
    #return render_template('home.html')
    left = [1, 2, 3, 4, 5]
    # heights of bars
    height = [10, 24, 36, 40, 5]
    # labels for bars
    tick_label = ['one', 'two', 'three', 'four', 'five']
    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])

    # # naming the y-axis
    # plt.ylabel('y - axis')
    # # naming the x-axis
    # plt.xlabel('x - axis')
    # # plot title
    # plt.title('My bar chart!')
    #
    # plt.savefig('static/images/plot.png')

    return render_template('home.html', url='/static/CVboiler.png')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

print("Hello, World")
