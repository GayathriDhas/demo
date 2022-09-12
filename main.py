{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fd6e0432-b220-4d49-aa87-b17d198bda6b",
   "metadata": {},
   "outputs": [],
   "source": [
    "import webapp2\n",
    "\n",
    "class MainHandler(webapp2.RequestHandler):\n",
    "    def get(self):\n",
    "        self.response.write('Hello YOUTUBE-new version')\n",
    "\n",
    "app = webapp2.WSGIApplication([\n",
    "    ('/',MainHandler)\n",
    "    ], debug=True)"
   ]
  }
 ],
 "metadata": {
  "environment": {
   "kernel": "python3",
   "name": "tf2-gpu.2-8.m95",
   "type": "gcloud",
   "uri": "gcr.io/deeplearning-platform-release/tf2-gpu.2-8:m95"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
